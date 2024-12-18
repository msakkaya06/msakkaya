import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { JwtHelperService } from "@auth0/angular-jwt";

import { map } from 'rxjs';
import { UserService } from './user.service';
import { Token } from '@angular/compiler';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  baseUrl: string = "http://localhost:5000/api/auth/";
  jwtHelper = new JwtHelperService();
  decodedToken: any;
  constructor(private http: HttpClient) { }

  login(model: any) {
    return this.http.post(this.baseUrl + 'login', model).pipe(
      map((response: any) => {
        const result = response;
        if (result) {
          localStorage.setItem("token", result.token);
          this.decodedToken = this.jwtHelper.decodeToken(result.token);

          console.log(this.decodedToken);
          
        }
      })
    )
  }

  register(model: any) {
    return this.http.post(this.baseUrl + 'register', model).pipe(
      map((response: any) => {
        const result = response;
        if (result) { localStorage.setItem("token", result.token)
        this.decodedToken = this.jwtHelper.decodeToken(result.token);
      }
      })
    )
  }

  loggedIn() {
    const token = localStorage.getItem("token");
    return !this.jwtHelper.isTokenExpired(token);
  }

  adminLogged(){
  
  const role=this.decodedToken.Role;
  if(role==="Admin")
  {return true;}
  return false;
  }
}
