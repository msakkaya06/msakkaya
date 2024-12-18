import { Component, OnInit } from '@angular/core';
import { AlertifyService } from '../_services/alertify.service';
import { AuthService } from '../_services/auth.service.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {
  constructor(public authService: AuthService, private alertify: AlertifyService,private router:Router) { }
  model: any = {};
 public userId:string='';
  ngOnInit(): void {
  }
  login() {
    this.authService.login(this.model).subscribe(next => {
     this.alertify.success("Giriş Başarılı, Hoşgeldiniz.")
      this.router.navigate(['/dashboard']);
    }, error => { this.alertify.error(error.error);
    console.log(error) })
  }
}
