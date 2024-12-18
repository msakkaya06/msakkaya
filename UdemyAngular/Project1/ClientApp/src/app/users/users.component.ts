import { Component, OnInit } from '@angular/core';
import { User } from '../_models/user';

import { UserService } from '../_services/user.service';
@Component({
  selector: 'users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {

  users: User[];
  selectedUser: User;

  constructor(private userService: UserService) { }

  ngOnInit(): void {




  }

  onSelectUser(user: User) {
    this.selectedUser = user;
  }
}


