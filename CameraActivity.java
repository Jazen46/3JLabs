public class CameraActivity extends Activity{

    private Camera mCamera;
    private CameraPreview mPreview;

    public void onCreate(Bundle savedInstanceState){
	super.onCreate(savedInstanceState);
	setContentView(R.layout.main);

	mCamera = getCameraInstance();

	mPreview = new CameraPreview(this,mCamera);
	
	//set preview as the content of our activiity
	FrameLayout preview = (FrameLayout) findViewById(R.id.camera_preview);
	preview.addView(mPreview);
    }


    
}
    