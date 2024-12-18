import { Component, OnInit } from '@angular/core';
import { AuthService } from './_services/auth.service';
import { JwtHelperService } from "@auth0/angular-jwt";
import { UserService } from './_services/user.service';
import { User } from './_models/user';
import { AlertifyService } from './_services/alertify.service';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})


export class AppComponent implements OnInit{
  title = 'LifeCoach';
  jwtHelper = new JwtHelperService();
  user: User;
username:string;
email:string;
  constructor(public authService: AuthService, public userService:UserService, private alertify:AlertifyService) { }
  ngOnInit() {
    const token = localStorage.getItem("token");
    if (token) { this.authService.decodedToken = this.jwtHelper.decodeToken(token);
      this.email=this.authService.decodedToken.email;
    this.userService.getUserByMail(this.email).subscribe(data => {this.username=data.username},error => { this.alertify.error(error); })
    }


  }
}
