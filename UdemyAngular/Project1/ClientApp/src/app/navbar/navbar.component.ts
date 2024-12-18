import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { error } from 'console';
import { User } from '../_models/user';
import { AlertifyService } from '../_services/alertify.service';

import { AuthService } from '../_services/auth.service';
import { UserService } from '../_services/user.service';
import { SignalrService } from '../_services/signalr.service';

@Component({
  selector: 'navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
mail: string;
 user:User;
username:string;
  model: any = {};
  users: User[];
  
  constructor(public authService: AuthService, public userService: UserService, private router: Router, private alertify: AlertifyService, private signalRService: SignalrService) { }

  ngOnInit(): void {

    }
  login() {
    this.authService.login(this.model).subscribe(next => {
     this.alertify.success("Giriş Başarılı, Hoşgeldiniz.")
      this.router.navigate(['/members']);
    }, error => { this.alertify.error(error); })

   

  }
  loggedIn() {

    return this.authService.loggedIn();

  }
  getUserByMail() {
    this.mail = this.authService.decodedToken.email;


  }
  getUsers() {
    this.userService.getUsers(this.authService.decodedToken.NameId).subscribe(users => {
      this.users = users;
    }, error => { this.alertify.error(error); })
  }

  logout() {
    localStorage.removeItem("token");
    this.alertify.warning("Çıkış Yaptınız!");
    this.router.navigate(['/home']);
    this.username='';
    this.signalRService.messages =[];
    this.signalRService.stopConnection();
    
}

adminLoggedIn() {

  return this.authService.adminLogged();

}



}



