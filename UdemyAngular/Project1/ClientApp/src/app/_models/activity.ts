import { Photo } from "./image";

export class Activity
{
    userId:number;
    activityId:number;
    description:string;
    startTime:Date;
    codeEnvironment:number;
    userProfileImageUrl:string;
    images:Photo[];
    userFirstName:string;
    userLastName:string;
    username:string;
    comments:Comment[];
    commentText:string;
    commentsCount:number;
    isMultiPhoto:boolean;

}

export class Comment{
    userFirstName:string;
    userLastName:string;
    username:string;
    userId: number;
    commentText:string;
    userProfileImageUrl:string;
    createdDate:Date;
    
}

// public int UiertId { get; set; }    
// public int ActivityId { get; set; }

// public string? Description { get; set; }

// public DateTime StartTime { get; set; }
// public int? CodeEnvironment { get; set; }
// public List<Images> Images { get; set; }