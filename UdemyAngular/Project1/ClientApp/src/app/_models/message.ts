export class Message{
  recipientId:number;
  text:string='';
}

export class MessageList{
  senderId:number;
  recipientId:number;
  senderFirstName:string;
  senderLastName: string;
  receivedFirstName:string;
  receivedLastName:string;
  senderProfileImageURL:string;
  receivedProfileImageURL:string;
  isSender:boolean;
  text:string;
  dateAdded:Date;
  isRead:boolean;
  data:[];

}

export class GetMessageParams
{
  currentUserId?:number;
  friendUserId?:number;
  }
export class SendMessageParams
{
  senderId:number;
  recipientId:number;
  text:string;
}

export class AuthMessage
{
  userId:number;
}

export class UsersConnectionIds
{
  userId:number;
  connectionId:string;
  connectedDate?:Date;
}
