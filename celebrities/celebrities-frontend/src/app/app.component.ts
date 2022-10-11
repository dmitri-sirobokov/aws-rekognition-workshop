import { Component } from '@angular/core';
declare const AWS: any;

const IDENTITY_POOL_ID = 'eu-central-1:79fc5267-f422-46e4-9669-64a034734a84';
const REGION = 'eu-central-1';
const BUCKET_NAME = 'rekognition-ninjava-unconference';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'celebrities-frontend';
  outputHtml = '';
  imageUrl = '';
  private files: FileList | null = null;
  private s3: any;

  constructor() {

    AWS.config.update({
        region: REGION,
        credentials: new AWS.CognitoIdentityCredentials({
            IdentityPoolId: IDENTITY_POOL_ID
        })
    });

    this.s3 = new AWS.S3({
        apiVersion: '2006-03-01',
        params: { Bucket: BUCKET_NAME }
    });


  }

  onFilesSelected(event: Event) {
    if (event.target != null) {
      this.files = (event.target as any).files as FileList;
    }
  }

  displayOutput() {
    this.outputHtml = '';
    this.imageUrl = 'https://' + BUCKET_NAME + '.s3.' + REGION + '.amazonaws.com/output/celeBoxed.jpg?' + new Date().getTime();
  }

  addPhoto() {
    if (!this.files?.length) {
        return alert('Please choose a file to upload first.');
    }
    var file = this.files[0];
    var fileName = file.name;
    var photoKey = 'input/' + fileName;
    this.s3.upload({
        Key: photoKey,
        Body: file,
        ACL: 'public-read'
    }, (err: any, data: any) => {
        if (err) {
            return alert('There was an error uploading your photo: ' + err.message);
        }
        this.outputHtml = 'Processing....';
        setTimeout(() => this.displayOutput(), 5000);
    });
}

}
