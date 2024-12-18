import { Component, OnInit } from '@angular/core';
import { AuthService } from '../_services/auth.service.service';
import { AlertifyService } from '../_services/alertify.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit{

  constructor(public authService: AuthService, private alertify:AlertifyService )
  {}
  ngOnInit(): void {
    
  }
  loggedIn() {

    return this.authService.loggedIn();

  }

  


logout() {
  localStorage.removeItem("token");
  this.alertify.warning("Çıkış Yaptınız!");
  // this.router.navigate(['/home']);

  
}

}
