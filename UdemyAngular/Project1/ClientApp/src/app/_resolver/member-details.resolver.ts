import { Injectable } from "@angular/core";
import { ActivatedRouteSnapshot, Resolve, Router, RouterStateSnapshot } from "@angular/router";
import { catchError, Observable, of } from "rxjs";
import { User } from "../_models/user";
import { AlertifyService } from "../_services/alertify.service";
import { AuthService } from "../_services/auth.service";
import { UserService } from "../_services/user.service";

@Injectable()
export class MemberDetailsResolver implements Resolve<User>
{
  constructor(private userService: UserService,private authService:AuthService, private route: Router, private alertify: AlertifyService){}

  resolve(route: ActivatedRouteSnapshot, state: RouterStateSnapshot):  | Observable<User> | Promise<User>{
     return this.userService
    .getUser(route.params['username'],this.authService.decodedToken.NameId)
    .pipe(catchError(error=>{
    this.alertify.error("Sunucu hatası oluştu");
    this.route.navigate(['/members']);
    return of();
   }));

  }

}
