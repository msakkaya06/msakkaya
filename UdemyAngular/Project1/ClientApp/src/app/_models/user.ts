
import { Image } from './image';
export class User
{
  email: string;
  id: number;
  username: string;
  firstName: string;
  lastName: string;
  age: number;
  created: Date;
  lastActive: Date;
  city: string;
  country: string;
  hobbies: string;
  educations:string;
  webSiteAdress:string;
  image: Image[];
  profileImageURL: string;
  introduction: string;
  isFollowing:boolean;
  newMessageCount:number;
  isNewMessage:boolean;
  followersCount:number;
  followingsCount:number;
}
