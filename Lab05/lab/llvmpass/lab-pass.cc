/*
  Ref:
  * https://llvm.org/doxygen/
  * https://llvm.org/docs/GettingStarted.html
  * https://llvm.org/docs/WritingAnLLVMPass.html
  * https://llvm.org/docs/ProgrammersManual.html
 */
#include "lab-pass.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Constants.h"
#include "llvm/IR/Value.h"

// #include <stdio.h>
#include <string.h>
#include <stdlib.h>

using namespace llvm;
using namespace std;

char LabPass::ID = 0;

bool LabPass::doInitialization(Module &M) {
  return true;
}

static Constant* getI8StrVal(Module &M, char const *str, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Constant *strConstant = ConstantDataArray::getString(ctx, str);

  GlobalVariable *gvStr = new GlobalVariable(M, strConstant->getType(), true,
    GlobalValue::InternalLinkage, strConstant, name);

  Constant *zero = Constant::getNullValue(IntegerType::getInt32Ty(ctx));
  Constant *indices[] = { zero, zero };
  Constant *strVal = ConstantExpr::getGetElementPtr(Type::getInt8PtrTy(ctx),
    gvStr, indices, true);

  return strVal;
}

static FunctionCallee printfPrototype(Module &M) {
  LLVMContext &ctx = M.getContext();

  FunctionType *printfType = FunctionType::get(
    Type::getInt32Ty(ctx),
    { Type::getInt8PtrTy(ctx) },
    true);

  FunctionCallee printfCallee = M.getOrInsertFunction("printf", printfType);

  return printfCallee;
}

static GlobalVariable* zeroGlobalVariable(Module &M, Twine const &name) {
  LLVMContext &ctx = M.getContext();

  Type* intType = Type::getInt32Ty(ctx);
  Constant* initialValue = ConstantInt::get(intType, 0);

  GlobalVariable* zgv = new llvm::GlobalVariable(
      M, intType, false, GlobalValue::InternalLinkage, initialValue, name);

  return zgv;
}

bool LabPass::runOnModule(Module &M) {
  errs() << "runOnModule\n";

  FunctionCallee printfCallee = printfPrototype(M); 
  GlobalVariable* blankspace = zeroGlobalVariable(M, "blankspace"); 

  for (auto &F : M) {
    if (F.empty()) {
      continue;
    }

    errs() << F.getName() << "\n";

    // insert after start of function
    BasicBlock &Bstart = F.front();
    Instruction &Istart = Bstart.front();
    IRBuilder<> BuilderStart(&Istart);

    // load original num and add 1
    Type* startType = BuilderStart.getInt32Ty();
    Value *before_add = BuilderStart.CreateLoad(startType, blankspace, "blankspace");
    ConstantInt* startone = BuilderStart.getInt32(1);
    Value *add = BuilderStart.CreateAdd(before_add, startone);
    BuilderStart.CreateStore(add, blankspace);

    // insert printf with original num * blank space
    Constant *num = getI8StrVal(M, "%*s", "num");
    Value* bs = BuilderStart.CreateGlobalString("");
    BuilderStart.CreateCall(printfCallee, { num, before_add, bs});

    // insert printf with function name and address
    Constant *func_name = getI8StrVal(M, "%s: %p\n" , "func_name");
    Value* name = BuilderStart.CreateGlobalString(F.getName());
    BuilderStart.CreateCall(printfCallee, { func_name, name, &F });

    // insert before end of function
    BasicBlock &Bend = F.back();
    Instruction &Iend = Bend.back();
    IRBuilder<> BuilderEnd(&Iend);

    // load original num and sub 1
    Type* endType = BuilderEnd.getInt32Ty();
    Value *before_sub = BuilderEnd.CreateLoad(endType, blankspace, "blankspace");
    ConstantInt* endone = BuilderEnd.getInt32(1);
    Value *sub = BuilderEnd.CreateSub(before_sub, endone);
    BuilderEnd.CreateStore(sub, blankspace);
  }

  return true;
}

static RegisterPass<LabPass> X("labpass", "Lab Pass", false, false);
