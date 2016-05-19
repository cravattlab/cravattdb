import {Pipe, PipeTransform} from '@angular/core';
import * as _ from 'lodash';

@Pipe({ name: 'groupByProtein' })
export class GroupByProteinPipe implements PipeTransform {
    transform(value: any, args?: any[]): Object[] {
        value = _.groupBy(value, 1);

        let keyArr = Object.keys(value),
            dataArr = [];

        keyArr.forEach(key => {
            dataArr.push({
                'uniprot': key,
                'symbol': value[key][0][2],
                'description': value[key][0][3],
                'mean': (value[key].reduce(
                    (a, b) => a + b[7], 0
                ) / value[key].length).toFixed(1),
                'value': value[key].map(d => d = d.slice(4))
            });
        });

        return dataArr;
    }
}