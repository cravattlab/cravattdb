export default class Utils {
    static specialMedian(ratios: number[]): number {
        // special empirical rule for weeding out false 20s
        if (ratios.length === 2 && ratios.indexOf(20) !== -1 && Math.min(...ratios) < 3) {
            return Math.min(...ratios);
        }

        try {
            // only get median of non-zero ratios
            return this.median(ratios.filter(x => x > 0));
        } catch (e) {
            return 0;
        }
    }

    static median(values: number[]): number {
        if (!values.length) {
            throw 'Cannot calculate median of empty array.';
        }

        // copy array before we sort so as to avoid mutating original
        let sorted = Array.from(values.values()).sort((a,b) => a - b);
        let half = Math.floor(values.length / 2);

        if (sorted.length % 2) {
            return sorted[half];
        } else {
            return (sorted[half - 1] + sorted[half]) / 2;
        }

    }
}
