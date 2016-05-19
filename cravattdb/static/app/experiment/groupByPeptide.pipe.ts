import {Pipe, PipeTransform} from '@angular/core';
import * as _ from 'lodash';

@Pipe({ name: 'groupByPeptide' })
export class GroupByPeptidePipe implements PipeTransform {
    transform(value: any, args?: any[]): Object[] {
        value = _.groupBy(value, 4);

        let keyArr = Object.keys(value),
            dataArr = [];

        keyArr.forEach(key => {
            dataArr.push({
                'groupKey': key,
                'symbol': value[key][0][2],
                'description': value[key][0][3],
                'mean': (value[key].reduce(
                    (a, b) => a + b[8], 0
                ) / value[key].length).toFixed(1),
                'value': value[key].map(d => d = [...d.slice(1,4), ...d.slice(5) ])
            });
        });

        return dataArr;
    }
}