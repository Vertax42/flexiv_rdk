import flexivrdk
import time

def grasp_cosmetic_box(robot, gripper, target_pose):
    """化妆品盒子抓取流程"""
    
    mode = flexivrdk.Mode
    
    # 1. 切换到笛卡尔力控模式
    robot.SwitchMode(mode.NRT_CARTESIAN_MOTION_FORCE)
    
    # 2. 设置柔顺性（避免碰撞时损坏）
    K_x = [2000, 2000, 500, 100, 100, 100]  # Z轴更柔软
    robot.SetCartesianImpedance(K_x)
    
    # 3. 打开夹爪
    gripper.Move(width=0.08, velocity=0.1)  # 80mm 开口
    time.sleep(1)
    
    # 4. 移动到盒子上方（纯运动控制）
    robot.SetForceControlAxis([False]*6)
    above_pose = target_pose.copy()
    above_pose[2] += 0.1  # Z 方向上升 10cm
    robot.SendCartesianMotionForce(above_pose)
    time.sleep(2)
    
    # 5. 下降接近盒子（Z轴力控）
    robot.SetForceControlAxis([False, False, True, False, False, False])
    robot.SendCartesianMotionForce(
        target_pose, 
        wrench=[0, 0, 3, 0, 0, 0]  # 3N 轻柔下压
    )
    time.sleep(2)
    
    # 6. 力控夹取
    gripper.Grasp(force=8.0)  # 8N 抓取力（根据盒子材质调整）
    time.sleep(1)
    
    # 7. 提起（纯运动控制）
    robot.SetForceControlAxis([False]*6)
    lift_pose = target_pose.copy()
    lift_pose[2] += 0.15
    robot.SendCartesianMotionForce(lift_pose)
    
    print("Grasp completed!")