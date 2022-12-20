import { Pipe, PipeTransform } from '@angular/core';
import { PLACEHOLDER_REGEXP } from '../services';

@Pipe({
  name: 'code'
})
export class CodePipe implements PipeTransform {
  transform(value?: string | null): string {
    if (!value) {
      return '';
    }
    return value
      .replace(PLACEHOLDER_REGEXP, '<strong>{$1}</strong>');
  }
}