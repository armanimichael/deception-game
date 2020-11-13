package web

import (
	"bufio"
	"fmt"
	"log"
	"net"
	"strings"
)

// Server contains information about the current Server
type Server struct {
	ConnType string
	ConnHost string
	ConnPort string
	Users    map[net.Addr]*User
}

// NewServer instantiate a new server
func NewServer(connType, connHost, connPort string) *Server {
	return &Server{
		ConnType: connType,
		ConnHost: connHost,
		ConnPort: connPort,
		Users:    make(map[net.Addr]*User),
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

		go newConnection(conn, s)
	}
}

func newConnection(conn net.Conn, s *Server) {
	addr := conn.RemoteAddr()
	log.Printf("User %v connected.", addr)

	// TODO Decode sent data and get username

	// Add user to user map
	user, ok := s.Users[addr]
	if !ok {
		user = &User{
			Conn:     conn,
			Username: "",
		}
	}
	s.Users[addr] = user

	for {
		msg, err := bufio.NewReader(conn).ReadString('\n')

		if err != nil {
			continue
		}

		// TODO: Find a better way to close server
		if strings.TrimRight(msg, "\r\n") == "leave" {
			log.Printf("User %v left.\n", addr)
			conn.Close()
			return
		}

		data := []byte(msg)
		s.broadcast(user, data)
	}
}

func (s *Server) broadcast(sender *User, msg []byte) {
	for addr, user := range s.Users {
		if addr != sender.Conn.RemoteAddr() {
			user.Conn.Write(msg)
		}
	}
}
