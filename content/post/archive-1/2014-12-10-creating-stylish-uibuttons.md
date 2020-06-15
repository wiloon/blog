---
title: Creating Stylish UIButtons
author: wiloon
type: post
date: 2014-12-10T00:50:42+00:00
url: /?p=7105
categories:
  - Uncategorized

---
http://code.tutsplus.com/tutorials/five-tips-for-creating-stylish-uibuttons&#8211;mobile-11847

Sometimes it only takes a few lines of code to make your interface pop. This tutorial will teach you five simple tricks for creating stylish UIButtons to make your app standout!
  
Subsequent Changes to Techniques & SoftwareCertain aspects of applications or techniques used in this tutorial have changed since it was originally published. This might make it a little difficult to follow along. We&#8217;d recommend looking at these more recent tutorials on the same topic:

Mobiletuts+ iOS SDK Category
  
Project Preview

Project Setup
  
In the download that accompanies this tutorial, you&#8217;ll find folders entitled "Initial Build&#8221; and "Final Build&#8221;. Rather than showing all the steps necessary to setup the initial project, you should simply download the attachment and follow along using the project from the "Initial Build&#8221; folder.

With the initial project open, go to the ViewController.m file and locate the forloop within the viewDidLoad method. The code snippets from the tips below should be placed within this loop.

Tip #1: Tweak Colors & Gradients
  
The most fundamental step toward customizing the UIButton class is to adjust the color of the background and title for both the default and highlighted states. The following code snippet sets each button&#8217;s background color to black, normal title color to white, and highlighted title color to red:

1
  
2
  
3
  
4
  
5
  
6
  
// Set the button Text Color
  
[btn setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
  
[btn setTitleColor:[UIColor redColor] forState:UIControlStateHighlighted];

// Set the button Background Color
  
[btn setBackgroundColor:[UIColor blackColor]];
  
Solid background colors are great, but a subtle gradient can often make the difference between bland and polished. Replace the setBackgroundColor:message above with the following to create a custom gradient:

1
  
2
  
3
  
4
  
5
  
6
  
7
  
8
  
// Draw a custom gradient
  
CAGradientLayer *btnGradient = [CAGradientLayer layer];
  
btnGradient.frame = btn.bounds;
  
btnGradient.colors = [NSArray arrayWithObjects:
  
(id)[[UIColor colorWithRed:102.0f / 255.0f green:102.0f / 255.0f blue:102.0f / 255.0f alpha:1.0f] CGColor],
  
(id)[[UIColor colorWithRed:51.0f / 255.0f green:51.0f / 255.0f blue:51.0f / 255.0f alpha:1.0f] CGColor],
  
nil];
  
[btn.layer insertSublayer:btnGradient atIndex:0];
  
Starting on line 4 above, an NSArray is created with the initial and target gradient colors. Note that the corresponding RGB values must be divided by 255 before being supplied to the colorWithRed:green:blue:alpha: message and that an alpha value of 1.0 represents fully opaque while an alpha value of 0.0 represents fully transparent. Unfortunately, a full explanation of the "magic&#8221; above is beyond the scope of this tutorial, but the important thing to remember is to that you simply need to replace the RGB values with the begin/end values you want to use in your own custom gradient.

If all went well, your menu should now look something like this:
  
Not bad, huh? And we&#8217;ve only just begun. . .

Tip #2: Round the Corners
  
Next we want to add a custom corner radius to each UIButton in order to make things look a bit more sleek. Insert the following lines of code to make this happen:

1
  
2
  
3
  
4
  
// Round button corners
  
CALayer *btnLayer = [btn layer];
  
[btnLayer setMasksToBounds:YES];
  
[btnLayer setCornerRadius:5.0f];
  
In line 4 above the corner radius is set to 5.0. Play with this number to increase or decrease how noticeable the corners appear.

You should now have a menu that looks just a bit slicker:
  
Tip #3: Add a Stroke Border
  
Sometimes the small tweaks make all the difference. Add a 1px, black stroke around each button with the following lines of code:

1
  
2
  
3
  
// Apply a 1 pixel, black border
  
[btnLayer setBorderWidth:1.0f];
  
[btnLayer setBorderColor:[[UIColor blackColor] CGColor]];
  
Can you tell the difference? It&#8217;s very subtle, but still valuable:
  
Tip #4: Use a Custom Font
  
Now let&#8217;s try a more noteworthy tweak. The default system font just isn&#8217;t cutting it. The game menu we&#8217;re building needs a font that can match the visual aesthetic of the game. A quick search on Google Fonts reveals just a font called Knewave by Tyler Finck that should do the trick. Download Knewave now.

After downloading the Knewave-Regular.ttf file, you&#8217;ll need to drag it into the Project Navigator pane in Xcode to add it to your project. Next, open up theInfo.plist file. Add a new property list row and type in "Fonts provided by application&#8221;. An array should be created automatically. Set the string associated with Item 0 to "Knewave-Regular.ttf&#8221;. Double check the name because the value is case sensitive. Save the file.

After making the above modification, your Info.plist file should now look like this:
  
Next, you&#8217;ll need to add the Knewave-Regular.ttf file to your project&#8217;s bundled resources. Select "SleekButtons&#8221; from the Project Navigator and then click the "Build Phases&#8221; tab. Expand the "Copy Bundle Resources&#8221; drop down and then click the plus sign.
  
At this point, you should be able to begin using the Knewave font in your project! Let&#8217;s test that out by jumping back to the ViewController.m file and modifying theviewDidLoad method to set a custom font:

01
  
02
  
03
  
04
  
05
  
06
  
07
  
08
  
09
  
10
  
// Set the button Text Color
  
[btn setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
  
[btn setTitleColor:[UIColor redColor] forState:UIControlStateHighlighted];

// Add Custom Font
  
[[btn titleLabel] setFont:[UIFont fontWithName:@&#8221;Knewave&#8221; size:18.0f]];

// Draw a custom gradient
  
CAGradientLayer *btnGradient = [CAGradientLayer layer];
  
btnGradient.frame = btn.bounds;
  
Notice that the fontWithName value is specified as "Knewave&#8221;, not "Knewave-Regular&#8221; as you might expect. This is because there is a difference between the font&#8217;s filename and the font&#8217;s given name. You&#8217;ll need to be sure you use the given name when working with your own fonts.

With the above code in place, the game menu should be complete! Build and run now and you should see something like the following:
  
Tip #5: Optional: Apply a Rotation
  
While not utilized in the primary design demonstrated by this tutorial, it&#8217;s often useful to apply a slight rotation to UIKit elements, particularly UIButton or UIImageobjects. Doing so is simple, and can be done with just one line of code.

You can try this out with the code written so far by doing the following:

1
  
2
  
3
  
4
  
5
  
6
  
7
  
self.startGameButton.transform = CGAffineTransformMakeRotation(M_PI / 180 * 5.0f);

for(UIButton *btn in buttons)
  
{
  
// Set the button Text Color
  
[btn setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
  
[btn setTitleColor:[UIColor redColor] forState:UIControlStateHighlighted];
  
In line 1 above, the constant M_PI is divided by 180 to generate 1 radian, which is then multiplied by 5.0f to result in a rotation of 5 radians. As you will notice if you build and run the project, the above is likely to result in anti-aliasing problems with UIKit elements that are drawn dynamically. Consequently, applying a rotation is more appropriate with a UIButton when the background image property is set and raster graphics are in use (i.e. this works best with PNG files).

Bonus Tip: Use UIButton-Glossy
  
With the five tips above, you&#8217;ve seen how easy it can be to make subtle yet significant tweaks to a UIButton object. However, what if I told you that doing so could be even easier? Meet UIButton-Glossy, an open-source category by George McMullen that automatically applies both a gradient and a glossy finish toUIButton objects.

Implementing UIButton-Glossy in your own project is simple. After you&#8217;vedownloaded the UIButton-Glossy.h and UIButton-Glossy.m files and added them to your Xcode project, import the *.h file in the main project view controller, like this:

1
  
2
  
#import "ViewController.h&#8221;
  
#import "UIButton+Glossy.h&#8221;
  
Now you can instantly apply a cool glossy effect on your buttons with just one line of code: [btn makeGlossy];.

To see this in action, replace the existing view controller code with the following:

01
  
02
  
03
  
04
  
05
  
06
  
07
  
08
  
09
  
10
  
11
  
12
  
13
  
14
  
15
  
for(UIButton *btn in buttons)
  
{
  
// Set the button Text Color
  
[btn setTitleColor:[UIColor whiteColor] forState:UIControlStateNormal];
  
[btn setTitleColor:[UIColor redColor] forState:UIControlStateHighlighted];

// Set default backgrond color
  
[btn setBackgroundColor:[UIColor blackColor]];

// Add Custom Font
  
[[btn titleLabel] setFont:[UIFont fontWithName:@&#8221;Knewave&#8221; size:18.0f]];

// Make glossy
  
[btn makeGlossy];
  
}
  
Your buttons should now have a glossy finish and the end result should look something like this:
  
Wrap Up
  
This tutorial has demonstrated multiple techniques for making custom UIButtonobjects shine. Download the attached project for a glimpse at the full, final source code.

Questions? Comments? Sound off below or message me directly@markhammonds.