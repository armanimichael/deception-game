package web

import (
	"dg-server/serialization"
	"errors"
	"fmt"
	"log"
	"net"
)

// Server contains information about the current Server
type Server struct {
	ConnType    string
	ConnHost    string
	ConnPort    string
	PlayerSlots uint8
	Users       map[net.Addr]*User
}

// NewServer instantiate a new server
func NewServer(connType, connHost, connPort string, playerSlots uint8) *Server {
	return &Server{
		ConnType:    connType,
		ConnHost:    connHost,
		ConnPort:    connPort,
		PlayerSlots: playerSlots,
		Users:       make(map[net.Addr]*User),
	}
}

// Run runs the Server on given protocol, host, and port
func (s *Server) Run() {
	host := fmt.Sprintf("%v:%v", s.ConnHost, s.ConnPort)
	listener, err := net.Listen(s.ConnType, host)

	if err != nil {
		log.Fatal("Error listening server: ", err.Error())
	}
	defer listener.Close()

	// Server Starting
	log.Printf("Listening on %v\n", listener.Addr())
	for {
		// Wait for Incoming Connections
		conn, err := listener.Accept()
		if err != nil {
			log.Fatal("Error accepting: ", err.Error())
			continue
		}

		go s.newConnection(conn)
	}
}

func (s *Server) newConnection(conn net.Conn) {
	addr := conn.RemoteAddr()
	err := s.newUserConnection(conn)
	if err != nil {
		log.Printf("User %v could not connect: %v", addr, err)
		return
	}

	for {
		data := serialization.NewDataFromClient()
		if err := data.Decode(conn); err != nil {
			log.Printf("Invalid data from %v: %v\n", addr, err)
			// TODO: Need more testing for users leaving correctly
			if conn.Close() == nil {
				delete(s.Users, addr)
			}
			return
		}

		// Creating user or refusing conn
		user, err := s.createNewUser(conn, data.Username)
		if err != nil {
			log.Printf("User %v cannot join, cloned or invalid username.\n", addr)
			conn.Write([]byte("This username is either invalid or already in use."))
			conn.Close()
			return
		}
		// User created
		log.Printf("User %v joined.\n", user.Username)

		// Actions
		switch data.Action {
		case "leave":
			log.Printf("User %v left.\n", user.Username)
			conn.Close()
			delete(s.Users, addr)
			return
		}
	}
}

func (s *Server) newUserConnection(conn net.Conn) error {
	// Check for max user connections
	if len(s.Users)+1 > int(s.PlayerSlots) {
		conn.Write([]byte("Server Full"))
		conn.Close()

		return errors.New("Server Full")
	} else if len(s.Users)+1 == int(s.PlayerSlots) {
		// TODO Populating the Gameboard once players joined
	}

	return nil
}

func (s *Server) createNewUser(conn net.Conn, username string) (*User, error) {
	// Add user to user map
	addr := conn.RemoteAddr()
	user, ok := s.Users[addr]
	if s.validateUsername(username) && !ok {
		// User doesn't exist - creating a new one
		user = &User{
			Conn:     conn,
			Username: username,
		}
		s.Users[addr] = user

		return user, nil
	}

	return nil, errors.New("user already exist")
}

func (s *Server) validateUsername(username string) bool {
	for _, user := range s.Users {
		if user.Username == username {
			return false
		}
	}

	return true
}

func (s *Server) broadcast(sender *User, msg []byte) {
	for addr, user := range s.Users {
		if addr != sender.Conn.RemoteAddr() {
			user.Conn.Write(msg)
		}
	}
}

func (s *Server) isServerFull() bool {
	return s.PlayerSlots == uint8(len(s.Users))
}
