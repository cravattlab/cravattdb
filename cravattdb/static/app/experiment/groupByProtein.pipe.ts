import {Pipe, PipeTransform} from '@angular/core';
import * as _ from 'lodash';

@Pipe({ name: 'groupByProtein' })
export class GroupByProteinPipe implements PipeTransform {
    transform(value: any, args?: any[]): Object[] {
        value = _.groupBy(value, 0);

        let keyArr = Object.keys(value),
            dataArr = [];

        keyArr.forEach(key => {
            dataArr.push({
                'groupKey': key,
                'symbol': value[key][0][1],
                'description': value[key][0][2],
                'mean': (value[key].reduce(
                    (a, b) => a + b[7], 0
                ) / value[key].length).toFixed(1),
                'columns': value[key].map(d => d = { data: d.slice(3, -2), ratio: d.slice(-2, -1), chromatogram: d.slice(-1) })
            });
        });

        return dataArr;
    }
}