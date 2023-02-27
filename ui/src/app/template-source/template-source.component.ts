import { Component, Input } from '@angular/core';

@Component({
  selector: 'td-template-source',
  templateUrl: './template-source.component.html',
  styleUrls: ['./template-source.component.scss']
})
export class TemplateSourceComponent {
  @Input() source?: string | null;
  @Input() file?: File;
}
