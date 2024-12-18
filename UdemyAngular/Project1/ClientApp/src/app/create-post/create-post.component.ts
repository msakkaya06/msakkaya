import { Component, OnDestroy, OnInit } from '@angular/core';
import { User } from '../_models/user';
import { Photo } from '../_models/image';
import { FileItem, FileUploader } from 'ng2-file-upload';
import { UserService } from '../_services/user.service';
import { ActivatedRoute } from '@angular/router';
import { AlertifyService } from '../_services/alertify.service';
import { AuthService } from '../_services/auth.service';
import { ActivityService } from '../_services/activity.service';
declare var jQuery: any;

@Component({
  selector: 'create-post',
  templateUrl: './create-post.component.html',
  styleUrls: ['./create-post.component.css']
})
export class CreatePostComponent implements OnInit {

  description: string;
  user: User;
  model: any = {}
  photos: Photo[] = [];
  uploader: FileUploader;
  hasBaseDropZoneOver = false;
  baseUrl = 'http://localhost:5000/api/';
  currentMain: Photo;
  userId: number;
  script: HTMLScriptElement;
  constructor(private userService: UserService,
    private authService: AuthService,
    private route: ActivatedRoute,
    private alertify: AlertifyService,
    private activityService:ActivityService
  ) {
    this.script = document.createElement("script");
    this.script.src = "../assets/scripts/ImageUpload.js";
    document.body.appendChild(this.script);
  }
  ngOnInit(): void {

    this.initializeUploader();

  }
  initializeUploader() {
    this.uploader = new FileUploader({
      url: this.baseUrl + 'photos/AddImage/' + this.authService.decodedToken.NameId,
      authToken: 'Bearer ' + localStorage.getItem('token'),
      isHTML5: true,
      allowedFileType: ['image'],
      autoUpload: false,
      removeAfterUpload: true,
      maxFileSize: 10 * 1024 * 1024,
      description:this.description
    }


    )
    this.uploader.onSuccessItem = (item, response, status, headers) => {
 
        if (response) {
          const res: Photo = JSON.parse(response);
          const photo = {
            id: res.id,
            url: res.url,
            dateAdded: res.dateAdded,
            description:this.uploader.options.description,
            isMain: true
          }
          photo.description=this.description;
          this.photos.push(photo);
        }

      
      this.uploader.onBuildItemForm = (item, form) => {
        form.append('Description', JSON.stringify(this.description));
    
      };

     

      this.uploader.onCompleteAll=()=>{
         console.log("işlem bitti");   
        console.log(this.photos);
     
        this.addActivity(this.photos);
        this.photos=[];
        
      }
      
      }   
  }

  addActivity(photos:Photo[])
  {
    this.activityService.addActivity(this.authService.decodedToken.NameId,photos).subscribe(result => {
      this.alertify.success("Gönderiniz başarıyla oluşturuldu")});

    
  }

  addActivityById(photoId:number[])
  {
    this.activityService.addActivityById(this.authService.decodedToken.NameId,photoId).subscribe(result => {
      this.alertify.success("Gönderiniz başarıyla oluşturuldu")});

    
  }
  ImgInit()


































  {
    this.initializeUploader()
  }

}



