class SpriteAnimation {
    constructor(app, sprite=null, removeOnEnd = false, cycled = false) {
        this.sprite = sprite;
        this.removeOnEnd = removeOnEnd;
        this.app = app;
        this.cycled = cycled;
        this.animations = [];
        this.currentAnimation = null;

    }

    setAnimation(positions, timestamps, easeFunc, textures) {
        this.maxTimestamp = timestamps[1];
        this.animations = [new SingleAnimation(positions, timestamps, easeFunc, this.sprite, textures)]; // positions e.g. {from: [50, 50], to: [100, 100]}
    }

    setAnimationSequence(positions, timestamps, easeFuncs) {
        // Length of the timestamps arr must be 1 more than length of the positions arr
        this.animations = [];
        this.maxTimestamp = timestamps[timestamps.length - 1];
        for (let a = 0; a < positions.length; a++) {
            this.animations.push(new SingleAnimation(
                positions[a],
                [timestamps[a], timestamps[a + 1]],
                easeFuncs[a]
            ));
        }
    }

    clearAnimations() {
        this.animations = [];
    }

    animationEnded(tick) {
        if (this.currentAnimation == null) {
            return true;
        }
        if (this.currentAnimation.timestamps[0] < tick ||
            this.currentAnimation.timestamps[1] >= tick) { // just in case
            return true;
        }
        return false;
    }

    findMatchingAnimation(tick) {
        // Select matching animation based on time, return true if there's one, otherwise return false.
        // If there's more than one, pick first
        for (let a = 0; a < this.animations.length; a++) {
            let animation = this.animations[a];
            if (animation.timestamps[0] < tick &&
                animation.timestamps[1] >= tick) {
                this.currentAnimation = animation;
                this.sprite.renderable = true;
                return true;
            }
        }
        this.currentAnimation = null;
        if (this.removeOnEnd) {
            this.sprite.renderable = false;
        }
        return false;
    }

    getTick(tick) {
        if (this.cycled) {
            return tick % this.maxTimestamp;
        }
        return tick;
    }

    frame(tick) {
        // call on each frame to set the position
        if (this.animationEnded(this.getTick(tick))) {
            this.findMatchingAnimation(this.getTick(tick));
        }
        if (this.currentAnimation !== null) {
            let pos = this.currentAnimation.calculatePosition(this.getTick(tick));
            if (this.sprite !== null) {
                this.sprite.x = pos[0];
                this.sprite.y = pos[1];
            }
        }
    }
}

class SingleAnimation {
    constructor(positions, timestamps, easeFunc, sprite = null, textures = []) {
        this.positions = positions;
        this.timestamps = timestamps;
        this.easeFunc = easeFunc;
        this.sprite = sprite;
        this.textures = textures;
    }

    calculatePosition(tick) {
        let animationLengthPos = [
            this.positions[1][0] - this.positions[0][0],
            this.positions[1][1] - this.positions[0][1]
        ];
        let animationLengthTime = this.timestamps[1] - this.timestamps[0];
        let tickRel = tick - this.timestamps[0];
        let animationProgress = tickRel / animationLengthTime;

        if (this.textures.length >= 1) {
            this.animateTexture(animationProgress);
        }

        let positionProgress = this.easeFunc(animationProgress);
        return [
            Math.floor(this.positions[0][0] + positionProgress * animationLengthPos[0]),
            Math.floor(this.positions[0][1] + positionProgress * animationLengthPos[1]),
        ];
    }

    animateTexture(animationProgress) {
        // animation progress is lower than 1 and bigger or equal 0. Animation length is divided into equal fragments
        let textureN = Math.floor(animationProgress * this.textures.length);
        if (textureN < 0 || textureN > this.textures.length) {return;}
        this.sprite.texture = this.textures[textureN];
    }
}

class Ease {
    static in_out(x) {
        // 0 <= x < 1
        return - (Math.cos(Math.PI * x) - 1) / 2;
    }
    static no_ease(x) {
        // 0 <= x < 1
        return x;
    }
    static in(x) {
        // 0 <= x < 1
        return 1 - Math.cos((x * Math.PI) / 2);
    }
    static out(x) {
        // 0 <= x < 1
        return Math.sin((x * Math.PI) / 2);
    }
}
