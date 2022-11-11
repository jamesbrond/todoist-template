import { Component, TemplateRef } from '@angular/core';
import { Toast } from 'src/app/interfaces';
import { ToasterService } from 'src/app/services';

@Component({
  selector: 'app-toast',
  templateUrl: './toast.component.html',
  styleUrls: ['./toast.component.scss']
})
export class ToastComponent  {

  constructor(public toaster: ToasterService) { }

  isTemplate(toast:Toast) {
		return toast.body instanceof TemplateRef;
	}

}
