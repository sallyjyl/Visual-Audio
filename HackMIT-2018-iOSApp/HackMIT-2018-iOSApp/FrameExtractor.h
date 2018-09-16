//
//  FrameExtractor.h
//  HackMIT-2018-iOSApp
//
//  Created by Ken Liu on 16/9/18.
//  Copyright © 2018 kenliu. All rights reserved.
//

#import <UIKit/UIKit.h>
#import <Foundation/Foundation.h>
#import <AVFoundation/AVFoundation.h>

@protocol MyDelegate <NSObject>
- (void) captured:(UIImage*) image;
@end

@interface FrameExtractor : NSObject <AVCaptureVideoDataOutputSampleBufferDelegate>

@property (strong, nonatomic) AVCaptureSession* captureSession;
@property (strong, nonatomic) dispatch_queue_t sessionQueue;
@property (strong, nonatomic) CIContext* context;

@property (weak) id<MyDelegate> delegate;

- (instancetype) init;

@end
