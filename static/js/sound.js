class SoundEffect {
    constructor(filename, delay) {
        this.audio = new Audio(filename);
        this.delay = delay;
        this.played = false;
    }

    frame(tick) {
        if (tick > this.delay && !this.played) {
            this.audio.play();
            this.played = true;
        }
    }
}