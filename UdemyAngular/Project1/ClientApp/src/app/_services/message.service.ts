import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { Observable } from "rxjs";
import { MessageList, UsersConnectionIds } from "../_models/message";
import { User } from "../_models/user";
import { AuthService } from "./auth.service";
import { SignalrService } from "./signalr.service";
@Injectable({
  providedIn: 'root'
})
export class MessageService {
  baseUrl: string = "http://localhost:5000/api/message/";
  public connectionId:any;
  

  constructor(private http: HttpClient,private authService:AuthService,private signalRService:SignalrService) { }

  sendMessage(recipientId: number,userId:number,messageText:string)
  {
   return this.http.post(this.baseUrl +"CreateMessage/"+ userId,{"recipientId":recipientId, "text":messageText});
  }

  getMessageUserList(userId:number):Observable<User[]>
  {
    return this.http.get<User[]>(this.baseUrl+'GetMessageUserList/' + userId);
  }

  getUsersChat(userId:number, friendUserId:number):Observable<MessageList[]>
  {
    return this.http.get<MessageList[]>(this.baseUrl+'GetUsersChat/' + userId + '/' + friendUserId);
  }

  setUsersConnectionIds()
  {
    // return this.http.post(this.baseUrl+"SetUsersConnectionIds",this.signalRService.usersConnectionIds)};
  }
}
