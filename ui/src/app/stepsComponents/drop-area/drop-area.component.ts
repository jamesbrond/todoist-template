import { Component, EventEmitter, Output } from '@angular/core';

export interface ReadedFile {
  file?: File;
  content?: string;
}

@Component({
  selector: 'td-drop-area',
  templateUrl: './drop-area.component.html',
  styleUrls: ['./drop-area.component.scss']
})
export class DropAreaComponent {
  @Output() data: EventEmitter<ReadedFile> = new EventEmitter<ReadedFile>();
  readedFile: ReadedFile = {}

  dragOver(e: DragEvent) {
    e.stopPropagation();
    e.preventDefault();
    e.dataTransfer!.dropEffect = 'copy';
  }

  drop(e: DragEvent) {
    e.stopPropagation();
    e.preventDefault();
    const dataTransfer = e.dataTransfer!;

    if (dataTransfer.files.length) {
      this.readedFile.file = dataTransfer.files[0];
      let reader = new FileReader();
      const self = this;
      reader.onloadend = function (onloadend) {
        let raw = (reader.result?.toString() || '').split(',');
          if (raw.length > 1) {
            self.readedFile.content = atob(raw[1]);
            self.data.emit(self.readedFile);
          }
      };

      // Read in the file as a data URL.
      reader.readAsDataURL(this.readedFile.file);
    } else {
      let raw = dataTransfer.getData('Text');
      if (raw) {
        this.readedFile.content = raw;
        this.data.emit(this.readedFile);
      }
    }
  }

  paste(e: ClipboardEvent) {
    e.stopPropagation();
    e.preventDefault();
    // get pasted data via clipboard API
    let clipboardData = e.clipboardData!;
    let pastedData = clipboardData.getData('Text');
    this.readedFile.content = pastedData;
    this.data.emit(this.readedFile);
  }

  fileSelected(e: any) {
    if (e.target.files && e.target.files.length) {
      const template_file = e.target.files[0];
      this.readedFile.file = template_file;
      let reader = new FileReader();
      const self = this;
      reader.onloadend = function (onloadend) {
        self.readedFile.content = reader.result?.toString();
        self.data.emit(self.readedFile);
      };
      reader.readAsText(template_file);
    }
  }
}

// ~@:-]