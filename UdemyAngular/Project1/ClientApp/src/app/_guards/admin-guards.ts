import { Injectable } from "@angular/core";
import { CanActivate, Router } from "@angular/router";
import { AuthService } from "../_services/auth.service";
@Injectable({providedIn:'root'})
export class AdminGuards implements CanActivate {

  constructor(private authService: AuthService, private router: Router) { }
  canActivate() {
    if (this.authService.adminLogged()) { return true; }
    this.router.navigate(['/home']);
    return false;
  }

  
}

