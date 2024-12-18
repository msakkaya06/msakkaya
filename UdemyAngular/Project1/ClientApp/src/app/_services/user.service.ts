import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError, map, Observable, Subject } from 'rxjs';
import { Model } from '../model';
import { User } from '../_models/user';


@Injectable({
  providedIn: 'root'
})
export class UserService {
  baseUrl: string = "http://localhost:5000/api/user";

  constructor(private http: HttpClient) { }

  getUsers(userId:number, followParams?:string):Observable<User[]>
  {
    if(followParams==="Followers")
    {
      return this.http.get<User[]>(this.baseUrl + '/GetUsers?UserId='+userId +'&&Followers=true');
    }
    if(followParams==="Followings")
    {
      return this.http.get<User[]>(this.baseUrl + '/GetUsers?UserId='+userId +'&&Followings=true');
    }

      return this.http.get<User[]>(this.baseUrl + '/GetUsers?UserId='+userId);

  }

  getUser(username:string, userId:number): Observable<User> {
    return this.http.get<User>(this.baseUrl + '/GetUser?username='+ username+'&&userId='+userId);
  }

  getUserByMail(email:string): Observable<User> {
    return this.http.get<User>(this.baseUrl + '/GetByMail?mail='+email);
  }



  updateUserProfile(user:User)
  {
    return this.http.put(this.baseUrl+'/UserProfileUpdate/',user);
  }

  followUser(followerId: number, userId:number, accountId:number)
  {
    return this.http.post(this.baseUrl +'/'+followerId +'/follow/'+ userId, {"accountId": accountId});
  }

unfollowUser(followerId: number, userId:number)
{
  return this.http.post(this.baseUrl +'/'+followerId +'/unfollow/'+ userId, {"accountId":userId});
}


}
