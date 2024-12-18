
export class Image {
  id: number;
  name: string;
  imageURL: string;
  description: string;
  dateAdded: Date;
  isProfile: boolean;
}

export class Photo {
    id:number;
    dateAdded:Date;
    description:string;
    isMain:boolean;
    url:string;

}

export class Ticket {
  constructor(public description: string = "") {}
}


