<?php
$oidir = 'OpenInviter';
include_once($oidir.'/openinviter.php');

// args
if($argc < 2) {
 echo 'Usage: php '.$argv[0]." -- <args>... \n";
 exit(1);
}

$inviter = new OpenInviter();

//print_r($argv);
switch($argv[2]) {
 /************
  * services *
  ************/
case '--services':
 $oi_services = $inviter->getPlugins();
 echo json_encode($oi_services);
 break;

 /************
  * contacts *
  ************/
case '--contacts':
 $email = $argv[3];
 $password = $argv[4];
 $provider = $argv[5];
 $ers = array();

 $inviter->startPlugin($provider);
 $internal = $inviter->getInternalError();

 if ($internal)
  $ers['inviter'] = $internal;
 elseif (!$inviter->login($email, $password))
 {
  $internal = $inviter->getInternalError();
  $ers['login'] = ($internal ? $internal : "Login failed. Please check the email and password you have provided and try again later");
 }
 elseif (false === $contacts = $inviter->getMyContacts())
  $ers['contacts'] = "Unable to get contacts.";
 else
 {
  $oi_session_id = $inviter->plugin->getSessionID();
 }
 $inviter->logout();

 $res = array();
 $res['errors'] = $ers;
 $res['contacts'] = $contacts;
 $res['oi_session_id'] = $oi_session_id;
 echo json_encode($res);
 break;

 /****************
  * send message *
  ****************/
case '--send-message':
 $subject = $argv[3];
 $body = $argv[4];
 $provider = $argv[5];
 $contacts = $argv[6];
 $email = $argv[7];
 $password = $argv[8];
 
 $ers = array();
 $res = array('result' => 1);

 $inviter->startPlugin($provider);
 $internal = $inviter->getInternalError();

 if ($internal)
  $ers['inviter'] = $internal;
 elseif (!$inviter->login($email, $password))
 {
  $internal = $inviter->getInternalError();
  $ers['login'] = ($internal ? $internal : "Login failed. Please check the email and password you have provided and try again later");
 }
 else {
  $oi_session_id = $inviter->plugin->getSessionID();
 }

 // send messages
 foreach (json_decode($contacts, true) as $k=>$v) {
  $mres = $inviter->sendMessage($oi_session_id, array('subject' => $subject, 'body' => $body), array($k, $v));
  if($mres == -1 || $mres === false) { // this plugin doesn't handle sending messages (not a social plugin) or the sending failed
   $res['result'] = $mres;
   break;
  }
 }
 $inviter->logout();

 $res['errors'] = $ers;
 echo json_encode($res);
 break;

}

