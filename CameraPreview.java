public class CameraPreview extends SurfaceView implements SurfaceHolder.Callback{
    private SurfaceHolder mHolder;
    private Camera mCamera;

    
    private boolean checkCameraHardware(Context c){
	if (context.getPackageManager().hasSystemFeature(PackageManager.FEATURE_CAMERA)){return true;}
	else{return false;}
    }
    
    
    public static Camera getCameraInstance(){
	Camera c = null;
	try{c = Camera.open();}//get Camera instance
	catch(Exception e){}//camera is either in use or does not exist
       	return c;
    }
    
    public CameraPreview(Context co, Camera ca){
	super(context);
	mCamera = camera;
	
	//Callback gives the client instructions on what to do with the surface
	//Holder controls the SV's underlying surface. Basically it "holds" the UI
	mHolder = getHolder();//get access to the Holder
	mHolder.addCallback(this);//add the Callback to the Holder
	mHolder.setType(SurfaceHolder.SURFACE_TYPE_PUSH_BUFFERS);//required on Android versions prior to 3.0
    }
    

    public void surfaceCreated(SurfaceHolder holder){
	try{//tell camera where to draw preview
	    mCamera.setPewviewDisplay(holder);
	    mCamera.startPreview();}
	catch(IOExpection e){
	    Log.d(TAG,"Error setting camera preview: "+e.Message());}
    }


    public void surfaceDestroyed(SurfaceHolder holder){
	if (mCamera != null){cCamera.stopPreview();}
    }

    public void surfaceChanged(SurfaceHolder holder, int format, int w, int h){
	if (mHolder.getSurface()==null){return;}
	
	//stop preview before making changes
	try {mCamera.stopPreview();}
	catch (Exception e){}
	
	//set preview size, resize rotate or reformatting changes here
	//temporarily unnecessary

	//restart preview
	try {
	    mCamera.setPreviewDisplay(mHolder);
	    mCmaera.startPreview();
	}catch {Exception 3){
	    Log.d(TAG,"Error starting camera preview: ":+e.getMessage());
	}
    }


    

}//end class
	
    
