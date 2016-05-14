export class Experiment {
    constructor(
        public name: string,
        public type: number,
        public organism: number,
        public probe?: number,
        public inhibitor?: number
    ) { }
}