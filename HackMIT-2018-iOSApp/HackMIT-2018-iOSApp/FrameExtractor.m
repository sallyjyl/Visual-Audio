//
//  FrameExtractor.m
//  HackMIT-2018-iOSApp
//
//  Created by Ken Liu on 16/9/18.
//  Copyright © 2018 kenliu. All rights reserved.
//

#import "FrameExtractor.h"

@implementation FrameExtractor

- (instancetype) init
{
    self = [super init];
    
    self.captureSession = [[AVCaptureSession alloc] init];
    self.sessionQueue = dispatch_queue_create("queue", DISPATCH_QUEUE_CONCURRENT);
    self.context = [[CIContext alloc] init];
    
    dispatch_async(self.sessionQueue, ^{
        [self configSession];
        [self.captureSession startRunning];
    });
    
    return self;
}


- (AVCaptureDevice*)selectCaptureDevice
{
    return [[AVCaptureDevice devices] filteredArrayUsingPredicate:<#(nonnull NSPredicate *)#>]
}


- (void) configSession
{
    self.captureSession.sessionPreset = AVCaptureSessionPresetLow;
    AVCaptureDevice* captureDevice = [AVCaptureDevice defaultDeviceWithMediaType:AVMediaTypeVideo];
    AVCaptureDeviceInput* captureDeviceInput = [AVCaptureDeviceInput deviceInputWithDevice:captureDevice error:nil];
    
    [self.captureSession addInput:captureDeviceInput];
    
    AVCaptureVideoDataOutput* videoOutput = [[AVCaptureVideoDataOutput alloc] init];
    [videoOutput setSampleBufferDelegate:self queue:self.sessionQueue];
    
    [self.captureSession addOutput:videoOutput];
    
    AVCaptureConnection* connection = [videoOutput connectionWithMediaType:AVMediaTypeVideo];
    connection.videoOrientation = AVCaptureVideoOrientationPortrait;
    [connection setVideoMirrored:YES];
    
}

- (UIImage*)imageFromSampleBuffer:(CMSampleBufferRef) sampleBuffer
{
    CVImageBufferRef imageBuffer = CMSampleBufferGetImageBuffer(sampleBuffer);
    CIImage* ciImage = [CIImage imageWithCVPixelBuffer:imageBuffer];
    
    CGImageRef cgImage = [self.context createCGImage:ciImage fromRect:ciImage.extent];
    return [UIImage imageWithCGImage:cgImage];
}

- (void) captureOutput:(AVCaptureOutput *)output didDropSampleBuffer:(CMSampleBufferRef)sampleBuffer fromConnection:(AVCaptureConnection *)connection
{
    UIImage* uiImage = [self imageFromSampleBuffer:sampleBuffer];
    dispatch_async(dispatch_get_main_queue(), ^{
        [self.delegate captured:uiImage];
    });
}



@end
