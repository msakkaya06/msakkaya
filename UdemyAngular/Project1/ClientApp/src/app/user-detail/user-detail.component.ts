import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { User } from '../_models/user';
import { AlertifyService } from '../_services/alertify.service';
import { AuthService } from '../_services/auth.service';
import { UserService } from '../_services/user.service';
import { FileUploader } from 'ng2-file-upload';
import { Image, Photo } from '../_models/image';



@Component({
  selector: 'user-detail',
  templateUrl: './user-detail.component.html',
  styleUrls: ['./user-detail.component.css']
})
export class UserDetailComponent implements OnInit {
 image:Image;
  user: User;
  model: any = {}
  photos: Photo[] = [];
  uploader: FileUploader;
  hasBaseDropZoneOver = false;
  baseUrl = 'http://localhost:5000/api/';
  currentMain: Photo;
  userId: number;
  
  constructor(private userService: UserService,private authService:AuthService, private route: ActivatedRoute, private alertify: AlertifyService) { }
  ngOnInit(): void { 
    this.route.data.subscribe(data => {this.user=data.user;});
    this.getUser();
    this.initializeUploader(); 
  }

  getUser() {
    this.userService.getUserByMail(this.authService.decodedToken.email).subscribe(user => { this.user = user; }, err => { this.alertify.error(err); });
  }

  updateUser()
  {console.log(this.user);
  this.userService.updateUserProfile(this.user).subscribe(()=>{this.alertify.success("Profiliniz Güncellendi")}, err=>{this.alertify.error(err);})
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
      description: "Profile Photo"
    }
    )
    this.uploader.onSuccessItem = (item, response, status, headers) => {
      
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
        this.alertify.success("Profil Fotoğrafınız Başarıyla Güncellendi");
   

      }
    }
   
  }
  uploadFile(){
    this.uploader.queue[0].upload();
    console.log(this.uploader.queue[0].url)
  }


}
  


