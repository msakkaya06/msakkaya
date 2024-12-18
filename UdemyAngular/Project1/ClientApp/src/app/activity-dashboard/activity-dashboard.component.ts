import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../_services/auth.service';
import { AlertifyService } from '../_services/alertify.service';
import { ActivityService } from '../_services/activity.service';
import { UserService } from '../_services/user.service';
import { Activity } from '../_models/activity';

@Component({
  selector: 'activity-dashboard',
  templateUrl: './activity-dashboard.component.html',
  styleUrls: ['./activity-dashboard.component.css']
})
export class ActivityDashboardComponent {
activities:Activity[];
commentText: string='';
  constructor (
    private userService: UserService,
    private route:ActivatedRoute,
    private authService:AuthService,
    private alertify: AlertifyService,
    private activityService:ActivityService){}

    ngOnInit(): void {
      this.getFollowingUsersActivity();
      

    }
    addComment(activityId:number, commentText:string)
    {
      this.activityService.addComment(activityId,this.authService.decodedToken.NameId,commentText).subscribe(result => {
        this.alertify.success("Yorumunuz Gönderildi")});
  
      
    }
    getFollowingUsersActivity()
    {
      this.activityService.getFollowingUsersActivity(this.authService.decodedToken.NameId).subscribe((activities => { this.activities = activities; }));
   
    }

}
