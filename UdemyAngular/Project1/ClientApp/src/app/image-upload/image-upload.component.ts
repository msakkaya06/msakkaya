import { Component, OnInit } from '@angular/core';
import { HttpEventType, HttpResponse } from '@angular/common/http';
import { Observable } from 'rxjs';


import { FileUploader } from 'ng2-file-upload'
import { AlertifyService } from '../_services/alertify.service'
import { AuthService } from '../_services/auth.service'
import { ActivatedRoute } from '@angular/router'
import { Photo } from '../_models/image';

@Component({
  selector: 'image-upload',
  templateUrl: './image-upload.component.html',
  styleUrls: ['./image-upload.component.css']
})
export class ImageUploadComponent implements OnInit {
  photos: Photo[] = [];
  uploader: FileUploader;
  hasBaseDropZoneOver = false;
  baseUrl = 'http://localhost:6001/api/';
  currentMain: Photo;
  currentCity: any;
  userId: number;

  imageInfos?: Observable<any>;
  constructor(private authService: AuthService,
    private alertifyService: AlertifyService,
    private activatedRoute: ActivatedRoute
  ) { }

  ngOnInit() {
    this.activatedRoute.params.subscribe(params => {
      this.currentCity = params["cityId"]
    })
    this.initializeUploader();
    this.userId = this.authService.decodedToken.NameId;
  }
  initializeUploader() {
    this.uploader = new FileUploader({
      url:this.baseUrl +'photos/'+this.authService.decodedToken.NameId,
      authToken: 'Bearer ' + localStorage.getItem('token'),
      isHTML5: true,
      allowedFileType: ['image'],
      autoUpload: false,
      removeAfterUpload: true,
      maxFileSize: 10 * 1024 * 1024,
      description: "this.description"
    }
    )
    this.uploader.onSuccessItem = (item, response, status, headers) => {
      console.log(status);
      if (response) {
        const res: Photo = JSON.parse(response);
        const photo = {
          id: res.id,
          url: res.url,
          dateAdded: res.dateAdded,
          description: res.description,
          isMain: true
          

        }
        this.photos.push(photo);
        console.log(res);

      }
    }
    console.log(this.photos);
  }

  uploadFile() {
    this.uploader.queue[0].upload();
    console.log(this.photos);
  }

}
