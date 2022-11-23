# Sample code for CS4283-5283
# Vanderbilt University
# Instructor: Aniruddha Gokhale
# Created: Fall 2022
# 
# Purpose: Provides the skeleton code for our custom transport protocol
#          For assignment 1, this will be a No-Op. But we keep the layered
#          architecture in all the assignments
#

# import the needed packages
import os     # for OS functions
import sys    # for syspath and system exception
import csv
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
import random
import concurrent.futures
from threading import Event
import heapq
import itertools

# add to the python system path so that packages can be found relative to
# this directory
sys.path.insert (0, "../")

from networklayer.CustomNetworkProtocol import CustomNetworkProtocol as NWProtoObj


FULL_PACKET_SIZE = 1024 # application request packet size of 1024 bytes
MTU = 16 # maximum transfer unit of 16 bytes
ack_list = []

def timer(self, choice):
    response = None
    print("do i ever enter timer")
    try:
      if choice == 3:
        print("sleeping to simulate drop")
        time.sleep(10)
        print("somehow finished sleeping")
      else:
        response = 1
    except Exception as e:
      print(e)
    finally:
      return response

def GetPaddedSegment(segment):
    segment_size = sys.getsizeof(segment)
    added_bits = FULL_PACKET_SIZE - segment_size
    need_to_add = bytes(added_bits)
    segment = segment + need_to_add
    #segment_size = sys.getsizeof(segment)
    #print(f"segment size: {segment_size}")
    return segment

def getChunks(segment, MTU):
  chunked_list = []
  for i in range(0, sys.getsizeof(segment), MTU):
    #chunk = segment[i:i+MTU]
    chunked_list.append(segment[i:i+MTU])
  return chunked_list



############################################
#       Custom Transport Protocol class
############################################
class CustomTransportProtocol ():
  '''Custom Transport Protocol'''



  ###############################
  # constructor
  ###############################
  def __init__ (self, role):
    self.role = role  # indicates if we are client or server, false => client
    self.ip = None
    self.port = None
    self.nw_obj = None # handle to our underlying network layer object

    self.config = None

    
  ###############################
  # configure/initialize
  ###############################
  def initialize (self, config, ip, port):
    ''' Initialize the object '''

    try:
      # Here we initialize any internal variables
      print ("Custom Transport Protocol Object: Initialize")
    
      # initialize our variables
      self.ip = ip
      self.port = port
      self.config = config


      # in a subsequent assignment, we will use the max segment size for our
      # transport protocol. This will be passed in the config.ini file.
      # Right now we do not care.
      
      # Now obtain our network layer object
      print ("Custom Transport Protocol::initialize - obtain network object")
      self.nw_obj = NWProtoObj ()
      
      # initialize it
      # 
      # In this assignment, we let network layer (which holds all the ZMQ logic) to
      # directly talk to the remote peer. In future assignments, this will be the
      # next hop router to whom we talk to.
      print ("Custom Transport Protocol::initialize - initialize network object")
      self.nw_obj.initialize (config, self.role, self.ip, self.port)
      
    except Exception as e:
      raise e  # just propagate it
  


  ##################################
  #  send application message
  ##################################
  def send_appln_msg (self, flag_split, dest_ip, dest_port, payload, size):

    protocol = self.config["Transport"]["TransportProtocol"]
      
    
    try:
      # @TODO@ Implement this
      # What we should get here is a serialized message from the application
      # layer along with the payload size. Now, depending on what is the
      # maximum segment size allowed by our transport, we will need to break the
      # total message into chunks of segment size and send segment by segment.
      # But we will do all this when we are implementing our custom transport
      # protocol. For Assignment #1, we send the entire message as is in a single
      # segment
      
      print ("Custom Transport Protocol::send_appln_msg")
      segment = str(flag_split) + "~" + dest_ip + "~" + str(dest_port) + "~" + payload + "###"
      
      segment = bytes(segment,"utf-8")
      segment = GetPaddedSegment(segment)

      print(f"Segment in transport layer {sys.getsizeof(segment)}")


      print(segment)
      if (flag_split):
        if protocol == "AlternatingBit":
          window_size = 1
          seq_num = 0
        
          chunked_list = getChunks(segment, MTU)
          print(chunked_list)
          for chunk in chunked_list:
            #choice = 2
            choice = random.randint(1,2)
            self.send_segment(choice, seq_num, chunk, size)
            print(f"chunk sending is {chunk}")
            #time.sleep(5)
            ack = self.nw_obj.recv_packet()
            '''while True:
              ack = self.nw_obj.recv_packet()
              try:
                with ThreadPoolExecutor(max_workers = window_size) as executor:
                  try:
                    future = executor.submit(timer, self, choice)
                    print(f"future = {future}")
                    response = future.result(timeout = 3)
                    if ack == seq_num or response != "None":
                      print("correct ack received")
                      seq_num = int(not(seq_num))
                    print(f"ack: {response}")
                  except concurrent.futures.TimeoutError:
                    print("Message timed out")
                  except Exception as e:
                    print("Unknown exception: {e}")
              except Exception as e:
                print(f"Unknown exception {e}")'''
            ack = ack.decode("utf-8")
            ack = int(ack)
            seq_num = int(seq_num)
            #ack = self.send_transport_ack(seq_num)
            #ack = self.recv_transport_ack()
            print(f"ack received is {ack} and {type(ack)}")
            print(f"seq num should be {seq_num} and {type(ack)}")

            if (ack != seq_num):
              print(f"wrong ack - {seq_num} expected, {ack} received")
            #time.sleep(5)
            seq_num = int(not(seq_num))
            
            # sending one segment at a time
            #self.send_segment(choice, seq_num, chunk, size)
            # wait until timeout or receives an ack
            # if timeout then resend chunk
            # else if ack has been received then move onto next chunk
    
        elif protocol == "GoBackN":
          print("in go back n")
          window_size = 8
          base = 0
          next_seq_num = 0
          seq_num = 0
          #choice = 1
          #choice = random.randint(1,2)
          buffer = []
          acks_recvd = []
          heapq.heapify(acks_recvd)
          j = 0 # chunk index for list
          chunked_list = getChunks(segment, MTU)
          #count = 0
          wrong_acks = 0
          flag_break = False
          while True:
            if flag_break:
              break
            j = j - wrong_acks
            print(f"wrong acks is {wrong_acks}")
            wrong_acks = 0
            print(f"what is my seq_num here: {seq_num}")
            print(f"what is my j here {j} and base is {base}")
            #time.sleep(5)
            acks_recvd = []
            count_window = 0
            for i in range(base, base + window_size):
              count_window = count_window + 1
              chunk = chunked_list[j]
              choice = random.randint(1,2)
              print(f"chunk sending is {chunk}")
              print(f"with seq num {seq_num}")
              self.send_segment(choice, seq_num, chunk, size)
              print(f"sending chunk {chunk} with seq_num {seq_num}")
              seq_num = seq_num + 1
              j = j + 1
              window_size = count_window
              print(f"count window is {count_window} and {window_size}")
              if j == 64:
                break
            #for i in range(i, i + window_size):
            count = 0
            print(f"window size is now {window_size}")
            while True:
              ack = self.nw_obj.recv_packet()
              ack = ack.decode("utf-8")
              ack = int(ack)
             
              heapq.heappush(acks_recvd, ack)
              print(f"received ack here as {ack}")
              count += 1
              if count == window_size:
                break
            '''for i in range(i, i + window_size):
              ack = self.nw_obj.recv_packet()
              ack = ack.decode("utf-8")
              ack = int(ack)
              heapq.heappush(acks_recvd, ack)
              print(f"received ack: {ack}")'''
            
            expected = list(range(0, window_size))
            print(f"expected is: {expected}")
            
            matching = []
            matching = list(itertools.zip_longest(expected, acks_recvd))
            print(f"matching: {matching}")
            end = window_size - 1
            print(f"end should be {end}")
            for exp, got in matching:
              if exp != got:
                base = exp
                print(f"missed ack: {exp}")
                #seq_num = exp
                seq_num = 0
                #time.sleep(5)
                slots_left = window_size - exp
                wrong_acks = slots_left
                #wrong_acks += 1 
                print(f"wrong acks is {wrong_acks}")
                #time.sleep(5)
                break
              else:
                base = exp
                
                
                
                print(f"new base is {base}")
                if exp == end:
                  base += 1
                  seq_num = 0 
                  #j = j - 1
                  print(f"got full window, base = {base}")
                  print(f"the seq_num is now {seq_num}")
                  print(f"the j now is: {j}")
                  if j == 64:
                    flag_break = True
                  #time.sleep(2)


          


            

            
            
         

          '''ack = ack.decode("utf-8")
          ack = int(ack)
          seq_num = int(seq_num)

            print(f"ack received is {ack} and {type(ack)}")
            print(f"seq num should be {seq_num} and {type(ack)}")

            if (ack != seq_num):
              print(f"wrong ack - {seq_num} expected, {ack} received")
            seq_num += 1
            # have a way to tell which seq_num have an ack
            # resend those with timeout 
            # once all have an ack then move window size to next 8 chunks
          print(f"chunked list: {chunked_list}")'''
          
        
        elif protocol == "SelectiveRepeat":
          window_size = 8
      
        #self.send_segment(choice, seq_num, segment, size)
      else:
        choice = 1
        seq_num = 0
        self.send_segment(choice, seq_num, segment, size)

        
    
      

    except Exception as e:
      raise e

  ##################################
  #  send transport layer segment
  ##################################
  def send_segment (self, choice, seq_num, chunk, len=0):
    protocol = self.config["Transport"]["TransportProtocol"]
    #print(chunk)
    try:
      # For this assignment, we ask our dummy network layer to
      # send it to peer. We ignore the length in this assignment
      print ("Custom Transport Protocol::send_segment")

      if protocol == "AlternatingBit" or protocol == "GoBackN":
          print("do alternating bit")
          if choice == 1:
              #print(f"sending chunk: {chunk} with seq_num {seq_num}")
              print("Send the chunk to the next hop")
              #print(f"what i am sending to network layer is {sys.getsizeof(chunk)}")
              #print(chunk)
              self.nw_obj.send_packet (seq_num, chunk, len)
          elif choice == 2:
              print("Delay sending chunk to the next hop")
              time.sleep(random.randint(1,3)) # delay for random integer from 1 to 10 
              self.nw_obj.send_packet (seq_num, chunk, len)
          elif choice == 3:
              print("Drop chunk")
              #self.nw_obj.send_packet(seq_num, chunk, len)

      #self.nw_obj.send_packet (segment, len)
      
    except Exception as e:
      raise e

  ######################################
  #  receive application-level message
  ######################################
  def recv_appln_msg (self, len=0):
    try:
      # The transport protocol (at least TCP) is byte stream, which means it does not
      # know the boundaries of the message. So it must be told how much to receive
      # to make up a meaningful message. In reality, a transport layer will receive
      # all the segments that make up a meaningful message, assemble it in the correct
      # order and only then pass it up to the caller.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::recv_appln_msg")
      appln_msg = self.recv_segment ()
      #print(f"now we have {appln_msg}")
      full_msg = []
      #appln_msg = []
      buffer = []


      if self.config["Transport"]["TransportProtocol"] == "AlternatingBit":
          print("alternating bit protocol")
          
      print(f"appln message: {appln_msg}")
      return appln_msg
    
    except Exception as e:
      raise e

  ######################################
  #  receive transport segment
  ######################################
  def recv_segment (self, len=0):
    try:
      # receive a segment. In future assignments, we may be asking for
      # a pipeline of segments.
      #
      # For this assignment, we do not care about all these things.
      print ("Custom Transport Protocol::recv_segment")
      segment = self.nw_obj.recv_packet (len)

      return segment
    
    except Exception as e:
      raise e


 
    

  ######################################
  #  send transport layer ack
  ######################################
  def send_transport_ack (self, seq_num):
    
    try:
      print ("Custom Transport Protocol::send_transport_ack")
      self.nw_obj.send_packet_ack(seq_num)
      
    except Exception as e:
      raise e