import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Message } from 'src/app/_models/message';
import { AuthService } from 'src/app/_services/auth.service';
import { MessageService } from 'src/app/_services/message.service';
import { User } from '../../_models/user';
import { AlertifyService } from '../../_services/alertify.service';
import { UserService } from '../../_services/user.service';
import { ActivityService } from 'src/app/_services/activity.service';
import { Activity } from 'src/app/_models/activity';

@Component({
  selector: 'member-details',
  templateUrl: './member-details.component.html',
  styleUrls: ['./member-details.component.css']
})
export class MemberDetailsComponent implements OnInit {
  user: User;
  followingUsers: User[];
  followerUsers: User[];
  followers: boolean = true;
  followings: boolean;
  messageText: string = '';
  activities:Activity[];
  commentText: string='';
  isMe:boolean;
  constructor
    (private userService: UserService,
      private route: ActivatedRoute,
      private authService: AuthService,
      private alertify: AlertifyService,
      private messageService: MessageService,
      private activityService: ActivityService) { }
  ngOnInit(): void {

    this.route.data.subscribe(data => { this.user = data.user; });
    if(this.user.id==this.authService.decodedToken.NameId)
    {
      this.isMe=true;
    }
    this.getUserFollowers(this.user.id);
    this.getUserFollowings(this.user.id);
    this.getUserActivity();
  }

  getUser() {
    this.userService.getUser(this.route.snapshot.params['username'], this.authService.decodedToken.NameId).subscribe(user => { this.user = user; }, err => { this.alertify.error(err); });
  }
  getUserActivity()
  {
    this.activityService.getUserActivity(this.user.id).subscribe((activities => { this.activities = activities; }));
 
  }


 
  addComment(activityId:number, commentText:string)
  {
    this.activityService.addComment(activityId,this.authService.decodedToken.NameId,commentText).subscribe(result => {
      this.alertify.success("Yorumunuz Gönderildi")});

    
  }
  unfollowUser(userId: number) {

    this.userService.unfollowUser(this.authService.decodedToken.NameId, userId).subscribe(result => {
      this.alertify.warning(this.user.username + ' kullanıcısını takibi bıraktın')
    },
      err => {
        this.alertify.error(err);
      });
    this.getUser();
    this.getUserFollowers(this.user.id);
    this.getUserFollowings(this.user.id);

  }

  followUser(userId: number) {

    this.userService.followUser(this.authService.decodedToken.NameId, userId, this.authService.decodedToken.NameId).subscribe(result => {
      this.alertify.success(this.user.username + ' kullanıcısını takip etmeye başladın')
    },
      err => {
        this.alertify.error(err);
      });
    this.getUser();
    this.getUserFollowers(this.user.id);
    this.getUserFollowings(this.user.id);

  }

  getUserFollowings(userId: number) {
    this.userService.getUsers(userId, "Followings").subscribe(users => { this.followingUsers = users; },
      err => { this.alertify.error(err); })

  }
  getUserFollowers(userId: number) {
    this.userService.getUsers(userId, "Followers").subscribe(users => { this.followerUsers = users; },
      err => { this.alertify.error(err); })

  }
  modalClosed(userId: number) {
    this.getUserFollowers(userId);
    this.getUserFollowings(userId);
  }

  sendMessage(recipientId: number, messageText: string) {
    this.messageService.sendMessage(recipientId, this.authService.decodedToken.NameId, messageText).subscribe(result => {
      this.alertify.success("Başarılı")
    },
      err => {
        this.alertify.error(err);
      });
  }

  closeMessageModal() {

  }

}
