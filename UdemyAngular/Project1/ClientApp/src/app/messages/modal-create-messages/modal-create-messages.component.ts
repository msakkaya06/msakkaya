import { Component, OnInit } from '@angular/core';
import { ModalService } from 'src/app/_modal';

@Component({
  selector: 'modal-create-messages',
  templateUrl: './modal-create-messages.component.html',
  styleUrls: ['./modal-create-messages.component.css']
})
export class ModalCreateMessagesComponent implements OnInit{



  bodyText: string;

    constructor(private modalService: ModalService) { }

    ngOnInit() {
        this.bodyText = 'This text can be updated in modal 1';
    }

    openModal(id: string) {
        this.modalService.open(id);
    }

    closeModal(id: string) {
        this.modalService.close(id);
    }
}
