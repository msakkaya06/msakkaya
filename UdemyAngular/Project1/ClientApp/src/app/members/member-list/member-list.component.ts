import { Component } from '@angular/core';
import { MessageList } from 'src/app/_models/message';
import { AuthService } from 'src/app/_services/auth.service';
import { User } from '../../_models/user';
import { AlertifyService } from '../../_services/alertify.service';
import { UserService } from '../../_services/user.service';

@Component({
  selector: 'member-list',
  templateUrl: './member-list.component.html',
  styleUrls: ['./member-list.component.css']
})
export class MemberListComponent {
  users: User[];


  constructor(private userService:UserService,private authService:AuthService, private alertify:AlertifyService) { }
  ngOnInit(): void { this.getUsers(); }

  getUsers() {
    this.userService.getUsers(this.authService.decodedToken.NameId).subscribe(users => {
      this.users = users;
    }, error => { this.alertify.error(error); })
  }

  getCurrentUserFollowings()
  {
    this.userService.getUsers(this.authService.decodedToken.NameId,"Followings").subscribe(users=>{this.users=users;},
      err=>{this.alertify.error(err);})

  }
  getCurrentUserFollowers()
  {
    this.userService.getUsers(this.authService.decodedToken.NameId,"Followers").subscribe(users=>{this.users=users;},
      err=>{this.alertify.error(err);})

  }

  followUser(userId:number){

    this.userService.followUser(this.authService.decodedToken.NameId,userId,this.authService.decodedToken.NameId).subscribe(result => {
      this.alertify.success("Takip işlemi başarılı")},
      err=>{this.alertify.error(err);
      });


  }
}
