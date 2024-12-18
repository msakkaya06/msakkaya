import { Component, OnInit } from '@angular/core';
declare var jQuery: any;

@Component({
  selector: 'create-activity',
  templateUrl: './create-activity.component.html',
  styleUrls: ['./create-activity.component.css']
})
export class CreateActivityComponent implements OnInit {
  script: HTMLScriptElement;
  constructor() {
    this.script = document.createElement("script");
    this.script.src = "../assets/scripts/ImageUpload.js";
    document.body.appendChild(this.script);
  }
  ngOnInit(): void {
  }

}
