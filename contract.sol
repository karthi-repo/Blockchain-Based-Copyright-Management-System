// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StoreCID {
  // Variable to store the CID
  string public cid;

  // Function to store a CID
  function storeCID(string memory _cid) public {
    cid = _cid;
  }
}
