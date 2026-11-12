#import <Cocoa/Cocoa.h>
@interface MOLauncher : NSObject <NSApplicationDelegate>
@property(strong) NSTask *task;
@end
@implementation MOLauncher
- (void)applicationDidFinishLaunching:(NSNotification *)note {
 NSString *script=[[[NSBundle mainBundle] resourcePath] stringByAppendingPathComponent:@"launch-game.sh"];
 self.task=[NSTask new]; self.task.launchPath=@"/bin/zsh"; self.task.arguments=@[script];
 self.task.terminationHandler=^(NSTask *task){ dispatch_async(dispatch_get_main_queue(), ^{
  if(task.terminationStatus!=0){NSAlert *a=[NSAlert new];a.messageText=@"心灵终结启动失败";a.informativeText=@"请查看 ~/Library/Application Support/MentalOmegaMacOriginal/启动日志.txt。";[a runModal];}
  [NSApp terminate:nil];
 });};
 NSError *error=nil;
 if(![self.task launchAndReturnError:&error]){NSAlert *a=[NSAlert new];a.messageText=@"无法启动心灵终结";a.informativeText=error.localizedDescription;[a runModal];[NSApp terminate:nil];}
}
@end
static MOLauncher *globalDelegate;
int main(int argc,const char **argv){@autoreleasepool{NSApplication *app=[NSApplication sharedApplication];MOLauncher *d=[MOLauncher new];globalDelegate=d;app.delegate=d;[app setActivationPolicy:NSApplicationActivationPolicyRegular];[app run];}return 0;}
