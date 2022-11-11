import { Injectable } from '@angular/core';
import { Toast } from '../interfaces';

@Injectable({
  providedIn: 'root'
})
export class ToasterService {

  toasts: Toast[] = [];

  log(body: string, options: any = {}) {
    this.toasts.push({ body, ...options });
  }

  error(body: string) {
    this.log(body, { classname: 'bg-danger text-light', delay: 15000 })
  }

  success(body: string) {
    this.log(body, { classname: 'bg-success text-light', delay: 10000 })
  }

  remove(toast: Toast) {
    this.toasts = this.toasts.filter(t => t !== toast);
  }

  clear() {
    this.toasts.splice(0, this.toasts.length);
  }
}
