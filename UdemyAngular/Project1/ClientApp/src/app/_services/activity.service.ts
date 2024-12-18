import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Activity } from '../_models/activity';
import { Observable } from 'rxjs';
import { Photo } from '../_models/image';

@Injectable({
  providedIn: 'root'
})
export class ActivityService{

  baseUrl: string = "http://localhost:5000/api/activity";

  constructor(private http: HttpClient) { }

  getFollowingUsersActivity(userId:number):Observable<Activity[]>
  {
   
      return this.http.get<Activity[]>(this.baseUrl + '/GetFollowingUsersActivity/'+userId);  
  }

  getUserActivity(userId:number):Observable<Activity[]>
  {
   
      return this.http.get<Activity[]>(this.baseUrl + '/GetUserActivity/'+userId);  
  }

  addComment(activityId:number,userId:number, commentText:string)
  {
    return this.http.post(this.baseUrl +'/AddComment/'+activityId+ '/'+ userId,{'commentText':commentText});

  }
  addActivity(userId:number, photos:Photo[])
  {
    return this.http.post(this.baseUrl +'/AddActivity/'+ userId,{'photoForCreationDto':photos});

  }

  addActivityById(userId:number, photoId:number[])
  {
    return this.http.post(this.baseUrl +'/AddActivityById/'+ userId,{'data':photoId});
  }

}
