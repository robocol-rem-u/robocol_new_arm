#include <ros/ros.h>
// #include <moveit/robot_model_loader/robot_model_loader.h>
// #include <moveit/robot_model/robot_model.h>
// #include <moveit/robot_state/robot_state.h>

int main(int argc,char** argv)
{
	ros::init(argc,argv,"inverseKinem");
	ros::AsyncSpinner spinner(1);
	spinner.start();
	ROS_INFO("Start.");

	// robot_model_loader::RobotModelLoader robot_model_loader("robot_description");
	// robot_model::RobotModelPtr kinematic_model = robot_model_loader.getModel();
	// ROS_INFO("Model frame: %s",kinematic_model->getModelFrame().c_str());

	ros::shutdown();
	return(0);
}