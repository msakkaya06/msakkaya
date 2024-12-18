import { Component, OnInit } from '@angular/core';
import { AlertifyService } from '../_services/alertify.service';
import { AuthService } from '../_services/auth.service.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  constructor(private alertify: AlertifyService, public authService:AuthService) { }
  ngOnInit(): void {

  }

  isLogged() {
    return this.authService.loggedIn();
  }
}
