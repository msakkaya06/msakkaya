import { Component, ElementRef, OnInit, ViewChild } from "@angular/core";
import { NgForm } from "@angular/forms";
import { Ticket } from "../_models/image";
import { UploadFileSimpleService } from "../_services/file-upload.service";
import { AlertifyService } from "../_services/alertify.service";


@Component({
  selector: "app-photo",
  templateUrl: "./photo.component.html",
  styleUrls: ["./photo.component.css"]
})
export class PhotoComponent implements OnInit {
  @ViewChild("screenshotInput") screenshotInput: ElementRef | null = null;
  model = new Ticket();

  constructor(
    private uploadService: UploadFileSimpleService,
    private alertify: AlertifyService
  ) { }

  ngOnInit() { }

  fileChange(event: any) {
    const filesList: FileList = event.target.files;
    console.log("fileChange() -> filesList", filesList);
  }

  submitForm(form: NgForm) {
    console.log("this.model", this.model);
    console.log("form.value", form.value);

    if (!this.screenshotInput) {
      throw new Error("this.screenshotInput is null.");
    }

    const fileInput: HTMLInputElement = this.screenshotInput.nativeElement;
    console.log("fileInput.files", fileInput.files);

    if (!fileInput.files) {
      return;
    }

    this.uploadService
      .postTicket(this.model, fileInput.files)
      .subscribe((data: any) => {
        console.log("success: ", data);
        this.alertify.success("Success!");
      }
        );
      }
  }
