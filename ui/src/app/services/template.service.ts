import { Injectable } from '@angular/core';
import { PlaceHolder } from '../types';

export const PLACEHOLDER_REGEXP = /{(\w+)\s*\|?\s*([^}]+)?}/g;

@Injectable({
  providedIn: 'root'
})
export class TemplateService {
  file?: File;
  private _template: string | null = null;
  private _placeHolders: PlaceHolder[] = [];

  set template(str: string | null) {
    this._template = str || '';
    // if template change placeholders are resetted
    this._placeHolders = this.getPlaceholders(str);
  }

  get template(): string | null {
    return this._template;
  }

  set placeHolders(value: PlaceHolder[]) {
    this._placeHolders = value;
  }

  get placeHolders(): PlaceHolder[] {
    return this._placeHolders;
  }

  getRenderedTemplate(): string | null {
    // return the template with the placeholders replaced by their values
    if (this._placeHolders && this._placeHolders.length) {
      let placeHoldersObject = this.getPlaceHoldersObject();

      let src = this._template || '';
      let matchesArray;
      while (matchesArray = PLACEHOLDER_REGEXP.exec(src)) {
        if (matchesArray.length) {
          src = src.replace(matchesArray[0], placeHoldersObject[matchesArray[1]])
        }
      }
      return src;
    }
    return this._template;
  }

  private getPlaceHoldersObject(): any {
    // from {key: 'key1', value: 'value1'} to {key1: 'value1'}
    let placeHoldersObject: any = {};
    this._placeHolders.forEach(p => placeHoldersObject[p.key] = p.value);
    return placeHoldersObject;
  }

  private getPlaceholders(template: string | null): PlaceHolder[] {
    if (!template) {
      return [];
    }
    let placeHolders: PlaceHolder[] = []
    let matchesArray;
    while (matchesArray = PLACEHOLDER_REGEXP.exec(template)) {
      if (matchesArray.length) {
        placeHolders.push({
          key: matchesArray[1],
          value: matchesArray[2] || ''
        });
      }
    }
    return placeHolders.filter((value, index, self) =>
    (index === self.findIndex((t) =>
      (t.key === value.key)
    ))
    );
  }

}
