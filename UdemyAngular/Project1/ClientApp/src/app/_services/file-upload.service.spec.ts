import { TestBed } from '@angular/core/testing';

import { UploadFileSimpleService } from './file-upload.service';

describe('FileUploadService', () => {
  let service: UploadFileSimpleService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(UploadFileSimpleService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
