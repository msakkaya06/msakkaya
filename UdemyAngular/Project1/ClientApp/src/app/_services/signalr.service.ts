import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import * as signalR from "@microsoft/signalr"
import { AuthMessage, GetMessageParams, MessageList, SendMessageParams, UsersConnectionIds } from '../_models/message';
import { request } from 'http';
import { error } from 'console';
import { Observable, Subject } from 'rxjs';
import { FriendListComponent } from '../friend-list/friend-list.component';
import { AuthService } from './auth.service';
import { User } from 'oidc-client';
import { MessageService } from './message.service';


@Injectable({
  providedIn: 'root'
})
export class SignalrService {
  public messages: MessageList[];
public usersConnectionIds: UsersConnectionIds=new UsersConnectionIds();
public connectionId:string;

  messageParam: GetMessageParams = new GetMessageParams();
  sendMessageParam:SendMessageParams = new SendMessageParams();
  messageParams: GetMessageParams[] = [];
  private sharedObj = new Subject<GetMessageParams>();
  constructor(private http: HttpClient, private authService: AuthService) { }


  public hubConnection: signalR.HubConnection;


  private startHttpRequest = () => {
    this.http.get('http://localhost:5000/api/userschat')
      .subscribe(res => {
       
      })
  }
  public startConnection = () => {
    this.hubConnection = new signalR.HubConnectionBuilder()
      .withUrl('http://localhost:5000/userschat/',
        {
          skipNegotiation: false
        })
      .withAutomaticReconnect()
      .build();
    this.hubConnection
      .start()
      .then(() => console.log('Connection started'))
      .catch(err => console.log('Error while starting connection: ' + err))
  }

  public stopConnection =() => {this.hubConnection.stop();}
  public userJoined= () => {
    this.hubConnection.on('userJoined',(data)=> 
    {
      this.mapUsersConnectionIds(data);
      this.hubConnection.invoke('UserJoinedBusiness', { UserId: this.usersConnectionIds.userId, ConnectionId: this.usersConnectionIds.connectionId});
    });
  }

  public userLeaved= () => {
    
    this.hubConnection.on('userLeaved',(data)=> 
    {
      this.mapUsersConnectionIds(data);
      this.hubConnection.invoke('UserLeavedBusiness', { UserId: this.usersConnectionIds.userId, ConnectionId: this.usersConnectionIds.connectionId});
    });
  }
  public addTransferChatDataListener = () => {

    this.hubConnection.on('transferchatdata', (data) => {
      this.messages = data;
     
    });
  }
  private mapReceivedMessage(CurrentUserId: number, FriendUserId: number) {
    this.messageParam.currentUserId = parseInt(this.authService.decodedToken.NameId);
    this.messageParam.friendUserId = FriendUserId;
    return this.messageParam
  }
  public mapUsersConnectionIds(connectionId:string) {
    this.usersConnectionIds.userId = parseInt(this.authService.decodedToken.NameId);
    this.usersConnectionIds.connectionId = connectionId;
 
    return this.usersConnectionIds
  }

  private mapSendMessage(recipientId: number, messageText: string) {
    this.sendMessageParam.recipientId =recipientId;
    this.sendMessageParam.senderId = parseInt(this.authService.decodedToken.NameId);
    this.sendMessageParam.text=messageText;
    return this.sendMessageParam
  }
  getUsersChatSendParams(CurrentUserId: number, friendUserId: number) {
    this.messageParam = this.mapReceivedMessage(CurrentUserId, friendUserId)
    this.hubConnection.invoke('GetUsersChatRTT', { CurrentUserId: this.messageParam.currentUserId, friendUserId: this.messageParam.friendUserId });
  }
  sendMessageRT(recipientId: number, text: string) {
    this.sendMessageParam=this.mapSendMessage(recipientId,text);
    this.hubConnection.invoke('CreateMessageRT', { recipientId: this.sendMessageParam.recipientId, Text: this.sendMessageParam.text, 
                                                  senderId:this.sendMessageParam.senderId});
  }

  public addBroadcastChartDataListener = () => {
    this.hubConnection.on('broadcastuserschat', (data) => {
      this.messages = data;
    })
  }

  public broadcastuserschat = () => {
    this.hubConnection.on('broadcastuserschat', (data) => {
      this.messages = data;
    })
  }
}

