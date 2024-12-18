import { Component, OnInit } from '@angular/core';

import { UserService } from '../_services/user.service';

@Component({
  selector: 'user-form',
  templateUrl: './user-form.component.html',
  styleUrls: ['./user-form.component.css']
})
export class UserFormComponent implements OnInit {

  constructor(private userService : UserService) { }

  ngOnInit(): void {
  }

}
